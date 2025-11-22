import Image from 'next/image';

export default function Header() {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    <div className="flex items-center">
                        <div className="relative w-10 h-10 mr-3">
                            <Image
                                src="/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"
                                alt="Proof of Talent Logo"
                                fill
                                className="object-contain"
                            />
                        </div>
                        <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                            Proof of Talent
                        </span>
                    </div>
                    {/* <nav className="hidden md:flex space-x-8">
                        <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors text-sm font-medium">How it Works</a>
                        <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors text-sm font-medium">Success Stories</a>
                        <a href="#" className="text-gray-600 hover:text-blue-600 transition-colors text-sm font-medium">FAQ</a>
                    </nav> */}
                </div>
            </div>
        </header>
    );
}
