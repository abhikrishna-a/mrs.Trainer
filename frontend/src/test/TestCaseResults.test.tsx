import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import TestCaseResults from '../components/TestCaseResults'
import type { TestCaseResult } from '../types/api'

const mockResults: TestCaseResult[] = [
  { passed: true, output: '4', expected: '4', error: '', status: 'ok', truncated: false },
  { passed: false, output: '5', expected: '3', error: '', status: 'ok', truncated: false },
]

describe('TestCaseResults', () => {
  it('renders passed/failed counts with verdict', () => {
    render(<TestCaseResults results={mockResults} verdict="accepted" />)
    expect(screen.getByText('1/2 passed')).toBeInTheDocument()
    expect(screen.getByText('Accepted')).toBeInTheDocument()
  })

  it('renders individual test cases', () => {
    render(<TestCaseResults results={mockResults} />)
    expect(screen.getByText('Test Case 1')).toBeInTheDocument()
    expect(screen.getByText('Test Case 2')).toBeInTheDocument()
  })

  it('renders error state', () => {
    render(<TestCaseResults results={[]} error="RuntimeError: division by zero" />)
    expect(screen.getByText('Execution Error')).toBeInTheDocument()
    expect(screen.getByText('RuntimeError: division by zero')).toBeInTheDocument()
  })

  it('returns null when no results and no error', () => {
    const { container } = render(<TestCaseResults results={[]} />)
    expect(container.innerHTML).toBe('')
  })
})
