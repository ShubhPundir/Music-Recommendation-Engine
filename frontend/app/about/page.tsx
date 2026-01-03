export default function About() {
    return (
        <div className="max-w-4xl mx-auto space-y-12 animate-in fade-in duration-700">

            {/* Header */}
            <div className="space-y-4 pb-8 border-b border-border">
                <h1 className="text-3xl font-bold font-serif tracking-tight">About the Project</h1>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    From a Big Data initiative to a full-scale deep learning research study.
                </p>
            </div>

            {/* Main Content */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-12">

                {/* Main Text Column */}
                <div className="md:col-span-2 space-y-8 text-base leading-7 text-muted-foreground">
                    <p>
                        This project began as a Big Data and Data Engineering initiative and evolved into a full-scale research study on music recommendation systems.
                        Over a span of four months, it investigated the end-to-end lifecycle of music platforms—focusing on how raw choices in data handling impact recommendation quality.
                    </p>
                    <p>
                        The goal is to bridge <strong className="font-semibold text-foreground">data engineering practices</strong> with <strong className="font-semibold text-foreground">machine learning research</strong>, demonstrating how low-level decisions—like ETL pipeline design and acoustic feature extraction—directly influence the performance of high-level recommendation models.
                    </p>

                    <div className="pt-4">
                        <h3 className="text-foreground font-semibold text-lg mb-4">Core Research Areas</h3>
                        <ul className="list-disc pl-5 space-y-2">
                            <li>Massive audio dataset management</li>
                            <li>Distributed ETL pipelines for metadata</li>
                            <li>Feature extraction from raw waveforms</li>
                            <li>Deep learning models for music understanding</li>
                        </ul>
                    </div>
                </div>

                {/* Sidebar / Integrations Column */}
                <div className="space-y-8">
                    <div className="p-6 bg-secondary/30 rounded-lg border border-border">
                        <h3 className="text-foreground font-semibold text-lg mb-4">Functional Integrations</h3>
                        <ul className="space-y-3 text-sm">
                            <li className="flex items-start gap-2">
                                <div className="h-1.5 w-1.5 mt-2 rounded-full bg-primary" />
                                <span>Raw Audio (WAV) Processing</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <div className="h-1.5 w-1.5 mt-2 rounded-full bg-primary" />
                                <span>Spectral Feature Analysis</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <div className="h-1.5 w-1.5 mt-2 rounded-full bg-primary" />
                                <span>Lyrics & Sentiment Pipelines</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <div className="h-1.5 w-1.5 mt-2 rounded-full bg-primary" />
                                <span>Deep Audio Embeddings</span>
                            </li>
                            <li className="flex items-start gap-2">
                                <div className="h-1.5 w-1.5 mt-2 rounded-full bg-primary" />
                                <span>Music Metadata (MusicBrainz)</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
