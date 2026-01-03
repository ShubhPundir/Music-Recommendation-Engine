interface TechStackBadgeProps {
    name: string;
    category?: 'api' | 'database' | 'tool';
}

export default function TechStackBadge({ name, category = 'tool' }: TechStackBadgeProps) {
    const colors = {
        api: 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800',
        database: 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-300 border-green-200 dark:border-green-800',
        tool: 'bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800',
    };

    return (
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${colors[category]}`}>
            {name}
        </span>
    );
}
