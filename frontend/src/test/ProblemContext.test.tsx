import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { ProblemProvider, useProblem } from '../context/ProblemContext'
import type { ReactNode } from 'react'

vi.mock('../api/client', () => ({
  default: {
    get: vi.fn(),
  },
}))

function wrapper({ children }: { children: ReactNode }) {
  return <ProblemProvider>{children}</ProblemProvider>
}

describe('ProblemContext polling', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('starts in idle state', () => {
    const { result } = renderHook(() => useProblem(), { wrapper })
    expect(result.current.taskId).toBeNull()
    expect(result.current.taskStatus).toBeNull()
    expect(result.current.taskResult).toBeNull()
    expect(result.current.language).toBe('python')
    expect(result.current.code).toBe('')
  })

  it('sets taskId and status when startPolling is called', () => {
    const { result } = renderHook(() => useProblem(), { wrapper })

    act(() => {
      result.current.startPolling('abc', false)
    })

    expect(result.current.taskId).toBe('abc')
    expect(result.current.taskStatus).toBe('PENDING')
    expect(result.current.taskResult).toBeNull()
  })

  it('resets state correctly', () => {
    const { result } = renderHook(() => useProblem(), { wrapper })

    act(() => {
      result.current.setCode('print("hello")')
      result.current.startPolling('abc', false)
    })

    expect(result.current.taskId).toBe('abc')
    expect(result.current.code).toBe('print("hello")')

    act(() => {
      result.current.reset()
    })

    expect(result.current.taskId).toBeNull()
    expect(result.current.taskStatus).toBeNull()
    expect(result.current.taskResult).toBeNull()
    expect(result.current.code).toBe('')
  })
})
