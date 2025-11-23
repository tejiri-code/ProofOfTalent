import Image from 'next/image';

export default function Header() {
    return (
        <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-md border-b border-gray-100">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-14 sm:h-16">
                    <div className="flex items-center">
                        <div className="relative w-8 h-8 sm:w-10 sm:h-10 mr-2 sm:mr-3">
                            <Image
                                src="/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"
                                alt="GtCompass Logo"
                                fill
                                className="object-contain"
                            />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-lg sm:text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                                GtCompass
                            </span>
                            <span className="text-[10px] sm:text-xs text-gray-500 -mt-1">Global Talent Compass</span>
                        </div>
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
