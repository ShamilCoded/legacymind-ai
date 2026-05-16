import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'LegacyMind AI - Understand Your Legacy Codebase with AI',
  description: 'AI-powered repository analysis providing architecture insights, dependency analysis, risk assessment, and modernization recommendations.',
  keywords: ['AI', 'code analysis', 'legacy code', 'repository analysis', 'modernization'],
  authors: [{ name: 'LegacyMind AI' }],
  openGraph: {
    title: 'LegacyMind AI',
    description: 'Understand Your Legacy Codebase with AI',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}

// Made with Bob
