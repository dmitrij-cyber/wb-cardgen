import React from 'react'

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { label: string }

export default function Button({ label, className, ...rest }: Props) {
  return (
    <button
      className={`px-4 py-2 rounded-2xl shadow bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 ${className || ''}`}
      {...rest}
    >
      {label}
    </button>
  )
}
