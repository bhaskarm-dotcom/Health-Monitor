import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AI Project Health Monitor',
  description: 'A preventive AI system that identifies project risks and provides actionable recommendations',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

