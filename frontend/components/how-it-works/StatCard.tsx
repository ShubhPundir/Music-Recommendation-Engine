import { LucideIcon } from 'lucide-react';

interface StatCardProps {
    icon: LucideIcon;
    label: string;
    value: string;
    iconColor?: string;
}

export default function StatCard({ icon: Icon, label, value, iconColor = 'text-primary' }: StatCardProps) {
    return (
        <div className="p-4 rounded-lg border border-border bg-card">
            <div className="flex items-center gap-2 mb-2">
                <Icon className={`h-5 w-5 ${iconColor}`} />
                <span className="font-semibold text-sm">{label}</span>
            </div>
            <p className="text-2xl font-bold">{value}</p>
        </div>
    );
}
