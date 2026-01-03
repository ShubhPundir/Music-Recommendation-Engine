import type { Metadata } from 'next';
import { Inter, Merriweather } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const merriweather = Merriweather({ weight: ['300', '400', '700'], subsets: ['latin'], variable: '--font-merriweather' });

export const metadata: Metadata = {
    title: 'Music Recommendation Engine Research',
    description: 'A Data Engineering & Deep Learning Research Project exploring scalable music recommendation systems.',
    keywords: ['Music Recommendation', 'Deep Learning', 'Data Engineering', 'Research', 'Audio Embeddings'],
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en" className={`${inter.variable} ${merriweather.variable}`}>
            <body className="min-h-screen flex flex-col bg-background font-sans text-foreground">
                <Navbar />
                <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {children}
                </main>
                <Footer />
            </body>
        </html>
    );
}
