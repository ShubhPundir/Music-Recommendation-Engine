interface DecisionCardProps {
    number: string;
    title: string;
    children: React.ReactNode;
}

export default function DecisionCard({ number, title, children }: DecisionCardProps) {
    return (
        <div className="space-y-4">
            <div className="flex items-baseline gap-3">
                <span className="text-3xl font-bold text-primary">{number}</span>
                <h3 className="text-xl font-semibold text-foreground">{title}</h3>
            </div>

            <div className="pl-12 space-y-3 text-base text-muted-foreground leading-relaxed">
                {children}
            </div>
        </div>
    );
}
