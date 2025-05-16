import { Ghost } from "lucide-react"

const AboutWidget = () => {
    return (
        <div className="bg-foreground p-3 rounded-[12px] shadow-lg w-full h-36">
            <h2 className="text-[16px] text-text font-sansation font-bold">About the project</h2>
            <Ghost className="text-text mt-4 mb-2" strokeWidth={2} size={50} />
        </div>
    );
}

export default AboutWidget;
