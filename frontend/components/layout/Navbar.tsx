'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { Menu, X, Music } from 'lucide-react';

const navigation = [
    { name: 'Home', href: '/' },
    { name: 'About', href: '/about' },
    { name: 'Research', href: '/research' },
    { name: 'How It Works', href: '/how-it-works' },
    { name: 'Literature Review', href: '/literature' },
];

export default function Navbar() {
    const pathname = usePathname();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <header className="bg-background border-b border-border sticky top-0 z-50">
            <nav className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Global">
                <div className="flex h-16 items-center justify-between">
                    <div className="flex lg:flex-1">
                        <Link href="/" className="-m-1.5 p-1.5 flex items-center gap-2">
                            <div className="p-1.5 bg-primary rounded-md">
                                <Music className="h-5 w-5 text-primary-foreground" />
                            </div>
                            <span className="font-serif font-bold text-lg tracking-tight">Music Recommendation Engine</span>
                        </Link>
                    </div>
                    <div className="flex lg:hidden">
                        <button
                            type="button"
                            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-muted-foreground hover:text-foreground"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                        >
                            <span className="sr-only">Open main menu</span>
                            {mobileMenuOpen ? (
                                <X className="h-6 w-6" aria-hidden="true" />
                            ) : (
                                <Menu className="h-6 w-6" aria-hidden="true" />
                            )}
                        </button>
                    </div>
                    <div className="hidden lg:flex lg:gap-x-8">
                        {navigation.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className={`text-sm font-medium transition-colors ${isActive ? 'text-primary' : 'text-muted-foreground hover:text-foreground'
                                        }`}
                                >
                                    {item.name}
                                </Link>
                            );
                        })}
                    </div>
                </div>
            </nav>
            {/* Mobile menu */}
            {mobileMenuOpen && (
                <div className="lg:hidden">
                    <div className="space-y-1 px-2 pb-3 pt-2 border-t border-border bg-background">
                        {navigation.map((item) => {
                            const isActive = pathname === item.href;
                            return (
                                <Link
                                    key={item.name}
                                    href={item.href}
                                    className={`block rounded-md px-3 py-2 text-base font-medium ${isActive ? 'bg-secondary text-primary' : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                                        }`}
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    {item.name}
                                </Link>
                            );
                        })}
                    </div>
                </div>
            )}
        </header>
    );
}
