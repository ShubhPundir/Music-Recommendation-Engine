import Link from 'next/link';
import { Database, Brain } from 'lucide-react';

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[calc(100vh-16rem)] text-center space-y-8 animate-in fade-in duration-700">
            <div className="space-y-4 max-w-3xl">
                <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl font-serif">
                    Music Recommendation Engine
                </h1>
                <h2 className="text-xl text-muted-foreground font-medium">
                    A Data Engineering & Deep Learning Research Project
                </h2>
            </div>

            <p className="max-w-2xl text-lg text-muted-foreground leading-relaxed">
                Exploring how large-scale audio data, metadata pipelines, and representation learning
                power modern music recommendation systems. From raw audio waveforms to similarity-driven recommendations.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Link
                    href="/about"
                    className="inline-flex items-center justify-center rounded-md bg-primary px-8 py-3 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                >
                    About the Project
                </Link>
                <Link
                    href="/research"
                    className="inline-flex items-center justify-center rounded-md border border-input bg-background px-8 py-3 text-sm font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                >
                    View Research Papers
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-16 text-left w-full max-w-4xl">
                <div className="p-6 rounded-lg border border-border bg-card text-card-foreground shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-md text-blue-600 dark:text-blue-400">
                            <Database className="h-5 w-5" />
                        </div>
                        <h3 className="font-semibold text-lg">Data Engineering</h3>
                    </div>
                    <p className="text-muted-foreground text-sm">
                        Scalable pipelines, metadata ingestion, and unified feature stores. Handling terabytes of structured and unstructured music data.
                    </p>
                </div>
                <div className="p-6 rounded-lg border border-border bg-card text-card-foreground shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-md text-purple-600 dark:text-purple-400">
                            <Brain className="h-5 w-5" />
                        </div>
                        <h3 className="font-semibold text-lg">Machine Learning</h3>
                    </div>
                    <p className="text-muted-foreground text-sm">
                        Deep audio representation learning, spectral analysis, and vector similarity search for content-based recommendations.
                    </p>
                </div>
            </div>
        </div>
    );
}
