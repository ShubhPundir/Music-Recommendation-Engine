import { BookOpen } from 'lucide-react';

interface Paper {
    id: string;
    title: string;
    authors: string;
    year: string;
    venue: string;
    focus: string;
}

interface LitReviewTableProps {
    papers: Paper[];
}

export default function LitReviewTable({ papers }: LitReviewTableProps) {
    return (
        <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-sm text-left">
                <thead className="bg-secondary text-secondary-foreground font-medium border-b border-border">
                    <tr>
                        <th className="px-6 py-4 font-semibold">Title</th>
                        <th className="px-6 py-4 font-semibold">Authors</th>
                        <th className="px-6 py-4 font-semibold w-24">Year</th>
                        <th className="px-6 py-4 font-semibold w-32">Venue</th>
                        <th className="px-6 py-4 font-semibold">Research Focus</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-border bg-card">
                    {papers.map((paper) => (
                        <tr key={paper.id} className="hover:bg-muted/50 transition-colors">
                            <td className="px-6 py-4 font-medium text-foreground">
                                <div className="flex items-start gap-2">
                                    <BookOpen className="h-4 w-4 mt-0.5 text-muted-foreground flex-shrink-0" />
                                    <span>{paper.title}</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-muted-foreground">{paper.authors}</td>
                            <td className="px-6 py-4 text-muted-foreground">{paper.year}</td>
                            <td className="px-6 py-4 text-muted-foreground">{paper.venue}</td>
                            <td className="px-6 py-4">
                                <span className="inline-flex items-center rounded-full border border-border bg-secondary px-2.5 py-0.5 text-xs font-semibold">
                                    {paper.focus}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
