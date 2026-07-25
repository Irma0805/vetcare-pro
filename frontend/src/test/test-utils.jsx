import { render } from '@testing-library/react'
import { MemoryRouter } from 'react-router'

function renderConRouter(ui, options) {
  return render(ui, { wrapper: MemoryRouter, ...options })
}

export * from '@testing-library/react'
export { renderConRouter }