import time
import requests
from django.conf import settings


class QuotaExceededException(Exception):
    pass


class CompilerRateLimitException(Exception):
    pass


LANGUAGE_MAP = {
    "python": "python-3.14",
}

# Filter by ENABLED_LANGUAGES — evaluated once at import; change requires server restart.
LANGUAGE_MAP = {k: v for k, v in LANGUAGE_MAP.items() if k in settings.ENABLED_LANGUAGES}


def execute_code(language, code, stdin=""):
    """Synchronous call to OnlineCompiler.io run-code-sync endpoint."""
    compiler = LANGUAGE_MAP.get(language)
    if not compiler:
        raise ValueError(f"Unsupported language: {language}")

    headers = {
        "Authorization": settings.ONLINECOMPILER_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "compiler": compiler,
        "code": code,
        "stdin": stdin,
    }

    last_status = None
    for attempt in range(3):
        try:
            resp = requests.post(
                settings.ONLINECOMPILER_API_URL,
                json=payload,
                headers=headers,
                timeout=60,
            )
        except requests.RequestException as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise

        last_status = resp.status_code

        if resp.status_code == 429:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise CompilerRateLimitException("Rate limited by OnlineCompiler.io")

        if resp.status_code in (402, 403):
            raise QuotaExceededException(f"Monthly quota exhausted (HTTP {resp.status_code})")

        resp.raise_for_status()
        break
    else:
        if last_status == 429:
            raise CompilerRateLimitException("Rate limited after retries")

    data = resp.json()
    output = data.get("output", "") or data.get("error", "") or ""

    truncated = False
    if len(output) > 999:
        output = output[:999]
        truncated = True

    return {
        "status": "success" if data.get("exit_code", -1) == 0 else "error",
        "output": output,
        "error": data.get("error", ""),
        "time": data.get("time", "0"),
        "memory": data.get("memory", "0"),
        "exit_code": data.get("exit_code", -1),
        "truncated": truncated,
    }


def run_test_cases(question, code, language, include_hidden=False):
    """Execute code against test cases sequentially."""
    test_cases = question.test_cases.all()
    if not include_hidden:
        test_cases = test_cases.filter(is_hidden=False)

    results = []
    for tc in test_cases:
        result = execute_code(language, code, tc.stdin)
        passed = (
            result["status"] == "success"
            and not result.get("truncated", False)
            and result["output"].strip() == tc.expected_output.strip()
        )
        results.append({
            "passed": passed,
            "output": result["output"],
            "expected": tc.expected_output,
            "error": result.get("error", ""),
            "time": result.get("time", "0"),
            "memory": result.get("memory", "0"),
            "exit_code": result.get("exit_code", -1),
            "truncated": result.get("truncated", False),
            "status": result["status"],
        })

    return results
