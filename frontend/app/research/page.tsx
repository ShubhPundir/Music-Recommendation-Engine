import PaperCard from '@/components/research/PaperCard';
import papersData from '@/data/papers.json';

interface Paper {
    type: string;
    theme: string;
    description: string;
    title: string;
    topics: string[];
    outcome: string;
}

export default function Research() {
    const papers = papersData as Paper[];

    return (
        <div className="space-y-12 animate-in fade-in duration-700">
            <div className="space-y-4 pb-8 border-b border-border">
                <h1 className="text-3xl font-bold font-serif tracking-tight">Research Papers</h1>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    In-depth analysis of Data Engineering pipelines and Deep Learning models for music recommendation.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {papers.map((paper) => (
                    <PaperCard
                        key={paper.theme}
                        title={paper.title}
                        theme={paper.theme}
                        description={paper.description}
                        topics={paper.topics}
                        type={paper.type as 'Data Engineering' | 'Machine Learning'}
                        outcome={paper.outcome}
                    />
                ))}
            </div>
        </div>
    );
}
