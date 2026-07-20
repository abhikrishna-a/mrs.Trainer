import Editor, { BeforeMount } from '@monaco-editor/react'

interface CodeEditorProps {
  language?: string
  value: string
  onChange?: (value: string | undefined) => void
  height?: string
}

export default function CodeEditor({ language = 'python', value, onChange, height = '60vh' }: CodeEditorProps) {
  const handleBeforeMount: BeforeMount = (monaco) => {
    monaco.editor.defineTheme('aptitude-dark', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'comment', foreground: '6A9955' },
        { token: 'keyword', foreground: 'C586C0' },
        { token: 'string', foreground: 'CE9178' },
        { token: 'number', foreground: 'B5CEA8' },
        { token: 'function', foreground: 'DCDCAA' },
      ],
      colors: {
        'editor.background': '#1e1e2e',
        'editor.foreground': '#e8e6e3',
        'editor.lineHighlightBackground': '#2a2a3e',
        'editor.selectionBackground': '#3a3a5e',
        'editorCursor.foreground': '#f0c040',
        'editorLineNumber.foreground': '#5e5c5c',
        'editorLineNumber.activeForeground': '#9a9797',
      },
    })
  }

  return (
    <Editor
      language={language}
      value={value}
      onChange={onChange}
      theme="aptitude-dark"
      beforeMount={handleBeforeMount}
      height={height}
      options={{
        minimap: { enabled: false },
        fontSize: 14,
        fontFamily: "'JetBrains Mono', 'Consolas', 'Courier New', monospace",
        fontLigatures: true,
        padding: { top: 16 },
        scrollBeyondLastLine: false,
        lineNumbers: 'on',
        tabSize: 4,
        renderWhitespace: 'selection',
        automaticLayout: true,
      }}
    />
  )
}
