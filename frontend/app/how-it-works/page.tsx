import Link from 'next/link';
import { ExternalLink, GitBranch, Users, Clock, Target, Lightbulb, TrendingUp } from 'lucide-react';

export default function HowItWorks() {
    return (
        <div className="max-w-5xl mx-auto space-y-16 animate-in fade-in duration-700">

            {/* Header */}
            <div className="space-y-6 pb-8 border-b border-border">
                <h1 className="text-4xl font-bold font-serif tracking-tight">How It Works</h1>
                <p className="text-xl text-muted-foreground leading-relaxed">
                    An 8-month journey from a Big Data experiment to a production-ready music recommendation system.
                </p>
            </div>

            {/* Project Overview */}
            <section className="space-y-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-md">
                        <GitBranch className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h2 className="text-2xl font-bold font-serif">The Project</h2>
                </div>

                <div className="prose prose-slate max-w-none">
                    <p className="text-base text-muted-foreground leading-relaxed">
                        The <Link href="https://github.com/ShubhPundir/Music-Recommendation-Engine" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline inline-flex items-center gap-1">
                            Music Recommendation Engine <ExternalLink className="h-3 w-3" />
                        </Link> was built by a team of 3 classmates over 8 months (on and off). We used it across multiple courses: <strong className="text-foreground">Big Data, Machine Learning, and Deep Learning</strong>.
                    </p>
                    <p className="text-base text-muted-foreground leading-relaxed">
                        What started as a Big Data + ML project evolved into a full recommendation system similar to what you'd see in a streaming app's "next song" logic.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                    <div className="p-4 rounded-lg border border-border bg-card">
                        <div className="flex items-center gap-2 mb-2">
                            <Users className="h-5 w-5 text-primary" />
                            <span className="font-semibold text-sm">Team Size</span>
                        </div>
                        <p className="text-2xl font-bold">3 Members</p>
                    </div>
                    <div className="p-4 rounded-lg border border-border bg-card">
                        <div className="flex items-center gap-2 mb-2">
                            <Clock className="h-5 w-5 text-primary" />
                            <span className="font-semibold text-sm">Duration</span>
                        </div>
                        <p className="text-2xl font-bold">8 Months</p>
                    </div>
                    <div className="p-4 rounded-lg border border-border bg-card">
                        <div className="flex items-center gap-2 mb-2">
                            <Target className="h-5 w-5 text-primary" />
                            <span className="font-semibold text-sm">Songs in DB</span>
                        </div>
                        <p className="text-2xl font-bold">1,100+</p>
                    </div>
                </div>
            </section>

            {/* Evolution */}
            <section className="space-y-6">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-md">
                        <TrendingUp className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                    </div>
                    <h2 className="text-2xl font-bold font-serif">How It Evolved</h2>
                </div>

                <div className="space-y-4 text-base text-muted-foreground leading-relaxed">
                    <p>
                        In the beginning, as someone who just got into how system design works for databases—while I was also working on making my own database from scratch side-by-side (<Link href="https://github.com/ShubhPundir/Find-DB" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline inline-flex items-center gap-1">
                            Find-DB <ExternalLink className="h-3 w-3" />
                        </Link>)—my simple goal was to put a ton of data and spread it into different tables and databases by some logic, just to get our hands dirty.
                    </p>

                    <div className="bg-muted/30 border-l-4 border-primary p-4 rounded-r-md">
                        <p className="font-semibold text-foreground mb-2">Data We Extracted:</p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li>Audio features from WAV files</li>
                            <li>Metadata about music (album, artist, track info)</li>
                            <li>Compiled spectrograms of music files</li>
                            <li>Extracted lyrics and sentiment analysis</li>
                            <li>Wave features and acoustic properties</li>
                        </ul>
                    </div>

                    <p>
                        Then it slowly evolved—we started putting ML into our pipeline for recommendations using different embeddings from WAV files, lyrics, and even vision transformers to predict the next sequence of songs.
                    </p>
                </div>
            </section>

            {/* My Role */}
            <section className="space-y-6">
                <h2 className="text-2xl font-bold font-serif">My Role & Responsibilities</h2>

                <div className="space-y-4 text-base text-muted-foreground leading-relaxed">
                    <p>
                        I was mainly responsible for <strong className="text-foreground">leading the team of 3</strong> for the data ingestion cycle and making strategic decisions by conducting a literature review study. The goal was to ensure we didn't fall into the same loop as other music recommendation projects using the same old techniques.
                    </p>

                    <p>
                        We evaluated different deep learning models and have sent <strong className="text-foreground">2 research papers</strong> for this project. We're expecting a response in <strong className="text-foreground">February 2026</strong>.
                    </p>

                    <div className="bg-secondary/50 p-6 rounded-lg border border-border">
                        <p className="font-semibold text-foreground mb-3">Scope Philosophy</p>
                        <p className="italic">
                            "There was no predefined spec. I decided what to build, how far to take it, and when to stop."
                        </p>
                    </div>
                </div>
            </section>

            {/* Key Decisions */}
            <section className="space-y-8">
                <div className="flex items-center gap-3 mb-4">
                    <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-md">
                        <Lightbulb className="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <h2 className="text-2xl font-bold font-serif">Key Strategic Decisions</h2>
                </div>

                <p className="text-muted-foreground">
                    Based on our literature review of papers less than 20 years old, we made three critical decisions:
                </p>

                {/* Decision 1 */}
                <div className="space-y-4">
                    <div className="flex items-baseline gap-3">
                        <span className="text-3xl font-bold text-primary">01</span>
                        <h3 className="text-xl font-semibold text-foreground">Treat This as a Data Engineering Problem First, ML Second</h3>
                    </div>

                    <div className="pl-12 space-y-3 text-base text-muted-foreground leading-relaxed">
                        <p>
                            We invested early in ETL and schema design to build a clean and stable data warehouse that could evolve with progressive needs and new findings.
                        </p>
                        <div className="bg-muted/30 p-4 rounded-md border-l-2 border-yellow-500">
                            <p className="font-semibold text-foreground mb-1">The Trade-off:</p>
                            <p>We sacrificed the first few months for slower visible progress because <strong className="text-foreground">recommendation quality is bounded by data quality</strong>. This made debugging in later stages much easier when tables failed to give expected results.</p>
                        </div>
                    </div>
                </div>

                {/* Decision 2 */}
                <div className="space-y-4">
                    <div className="flex items-baseline gap-3">
                        <span className="text-3xl font-bold text-primary">02</span>
                        <h3 className="text-xl font-semibold text-foreground">Use Content-Based Similarity Over Collaborative Filtering</h3>
                    </div>

                    <div className="pl-12 space-y-3 text-base text-muted-foreground leading-relaxed">
                        <p>
                            One of the most regrettable parts: <strong className="text-foreground">we could not get real data for user interactions</strong> with the music.
                        </p>
                        <p>
                            In our efforts to falsify fake data for user interactions, we realized that compiling the scale of fake users to mimic these interactions would consume the vast majority of our time. So we had to drop user interaction data.
                        </p>
                        <div className="bg-blue-50 dark:bg-blue-950/20 p-4 rounded-md">
                            <p className="font-semibold text-foreground mb-1">Testing Approach:</p>
                            <p>For all testing purposes, each of the 3 group members generated <strong className="text-foreground">10 playlists each</strong> from the 1,100 songs in our database.</p>
                        </div>
                    </div>
                </div>

                {/* Decision 3 */}
                <div className="space-y-4">
                    <div className="flex items-baseline gap-3">
                        <span className="text-3xl font-bold text-primary">03</span>
                        <h3 className="text-xl font-semibold text-foreground">Hybrid Framework Beyond Spectrogram-Based CNNs</h3>
                    </div>

                    <div className="pl-12 space-y-3 text-base text-muted-foreground leading-relaxed">
                        <p>
                            We built a <strong className="text-foreground">continuous voting ensembler</strong> where each feature set had different weights contributing to similarity from the last <em>n</em> songs played.
                        </p>
                        <p>
                            With the diverse dataset we acquired for each song, this approach helped connect every dot for the next potential song recommendation.
                        </p>
                    </div>
                </div>
            </section>

            {/* Future Plans */}
            <section className="space-y-6">
                <h2 className="text-2xl font-bold font-serif">Future Plans (Phase 3)</h2>

                <div className="space-y-4 text-base text-muted-foreground leading-relaxed">
                    <p>
                        We envision adding a <strong className="text-foreground">real-time interface</strong> to capture whether music is liked or not via implicit + explicit features like:
                    </p>

                    <ul className="list-disc pl-6 space-y-2">
                        <li>Skipping the song</li>
                        <li>Skipping parts of it</li>
                        <li>Replay behavior</li>
                        <li>Volume adjustments</li>
                    </ul>

                    <p>
                        This would cater to <strong className="text-foreground">taste first and labels later</strong>. Unfortunately, due to time and effort constraints, we couldn't achieve this.
                    </p>

                    <div className="bg-muted/30 p-6 rounded-lg border border-border">
                        <p className="font-semibold text-foreground mb-3">The Challenge:</p>
                        <p>
                            Each music data point containing such a diverse feature set means the periodic computation required for a song would be very <strong className="text-foreground">computationally expensive</strong>.
                        </p>
                        <p className="mt-3">
                            From our research, a <strong className="text-foreground">periodic time queue</strong> for songs would be carried out in a horizontally scaled way to update the social dynamics of the song. To keep things light on the user end, the updated model would be the new federated model for all until its next cycle of update.
                        </p>
                        <p className="mt-3 text-sm">
                            These update cycles should be based on factors like streaming frequency, jumps of hype, popularity, etc.
                        </p>
                    </div>
                </div>
            </section>

            {/* Results */}
            <section className="space-y-6 pb-8">
                <h2 className="text-2xl font-bold font-serif">What We Shipped</h2>

                <div className="bg-gradient-to-r from-primary/10 to-purple-500/10 p-8 rounded-lg border border-primary/20">
                    <p className="text-lg text-foreground leading-relaxed">
                        We shipped a <strong>working internal recommendation system</strong> that could generate next-song predictions from any playlist in <strong className="text-primary">under 4 seconds</strong>.
                    </p>
                    <p className="text-base text-muted-foreground mt-4">
                        While it wasn't production-ready for consumers, it was stable enough that all three of us used it regularly to evaluate recommendation quality and debug failures.
                    </p>
                    <p className="text-base text-foreground font-semibold mt-6">
                        The biggest win? How quickly we could iterate on features because of the data foundation we built early.
                    </p>
                </div>
            </section>

        </div>
    );
}
