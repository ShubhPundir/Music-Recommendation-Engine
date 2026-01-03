import LitReviewTable from '@/components/research/LitReviewTable';
import litReviewData from '@/data/lit-review.json';

export default function Literature() {
    return (
        <div className="space-y-12 animate-in fade-in duration-700">
            <div className="space-y-4 pb-8 border-b border-border">
                <h1 className="text-3xl font-bold font-serif tracking-tight">Literature Review</h1>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    A curated list of foundational research in Music Information Retrieval and Audio Representation Learning.
                </p>
                <div className="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium text-muted-foreground ring-1 ring-inset ring-gray-500/10">
                    View Only • Read Mode
                </div>
            </div>

            <LitReviewTable papers={litReviewData} />
        </div>
    );
}
