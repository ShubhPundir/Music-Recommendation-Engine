export default function Footer() {
    return (
        <footer className="bg-background border-t border-border mt-auto">
            <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
                <div className="md:flex md:items-center md:justify-between">
                    <div className="flex justify-center md:justify-start space-x-6 md:order-2">
                        <span className="text-sm text-muted-foreground">Data Engineering</span>
                        <span className="text-sm text-muted-foreground">•</span>
                        <span className="text-sm text-muted-foreground">Machine Learning</span>
                        <span className="text-sm text-muted-foreground">•</span>
                        <span className="text-sm text-muted-foreground">Deep Learning</span>
                    </div>
                    <div className="mt-8 md:order-1 md:mt-0">
                        <p className="text-center text-xs leading-5 text-muted-foreground md:text-left">
                            &copy; {new Date().getFullYear()} Music Recommendation Engine Research Project.
                            <br className="hidden md:inline" /> Built as an academic and applied research initiative.
                        </p>
                    </div>
                </div>
            </div>
        </footer>
    );
}
