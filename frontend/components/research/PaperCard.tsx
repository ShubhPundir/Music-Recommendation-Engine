import { Database, Brain } from 'lucide-react';

interface PaperCardProps {
    title: string;
    theme: string;
    description: string;
    topics: string[];
    type: 'Data Engineering' | 'Machine Learning';
    outcome: string;
}

export default function PaperCard({ title, theme, description, topics, type, outcome }: PaperCardProps) {
    const isML = type === 'Machine Learning';
    const Icon = isML ? Brain : Database;

    return (
        <div className="flex flex-col h-full rounded-lg border border-border bg-card text-card-foreground shadow-sm hover:shadow-md transition-shadow">
            <div className="p-6 flex-1 space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between gap-4">
                    <div className="space-y-1">
                        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                            <Icon className="h-4 w-4" />
                            {type}
                        </div>
                        <h3 className="font-semibold text-xl leading-tight font-serif">{theme}</h3>
                    </div>
                </div>

                {/* Description */}
                <div className="text-sm text-muted-foreground leading-relaxed">
                    <p className="mb-2 font-medium text-foreground">{title}</p>
                    <p>{description}</p>
                </div>

                {/* Topics */}
                <div className="flex flex-wrap gap-2 pt-2">
                    {topics.map((topic) => (
                        <span
                            key={topic}
                            className="inline-flex items-center rounded-md border border-border bg-secondary px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                        >
                            {topic}
                        </span>
                    ))}
                </div>
            </div>

            {/* Footer / Outcome */}
            <div className="p-6 pt-0 mt-auto">
                <div className="rounded-md bg-muted/50 p-4 text-sm">
                    <span className="font-semibold block mb-1">Outcome:</span>
                    <span className="text-muted-foreground">{outcome}</span>
                </div>
            </div>
        </div>
    );
}
