import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Analytics } from "@vercel/analytics/next"

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "GtCompass - Global Talent Compass | UK Global Talent Visa Assessment",
  description:
    "AI-powered assessment for the UK Global Talent Visa. Get a detailed roadmap in minutes.",
  openGraph: {
    title: "GtCompass - Global Talent Compass | UK Global Talent Visa Assessment",
    description:
      "AI-powered assessment for the UK Global Talent Visa. Get a detailed roadmap in minutes.",
    images: ["/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"],
  },
  twitter: {
    card: "summary_large_image",
    title: "GtCompass - Global Talent Compass | UK Global Talent Visa Assessment",
    description:
      "AI-powered assessment for the UK Global Talent Visa. Get a detailed roadmap in minutes.",
    images: ["/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png"],
  },
  icons: {
    icon: [
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '16x16', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '32x32', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '96x96', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: 'any', type: 'image/svg+xml' },
    ],
    apple: [
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '57x57', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '60x60', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '72x72', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '76x76', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '114x114', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '120x120', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '144x144', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '152x152', type: 'image/png' },
      { url: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png', sizes: '180x180', type: 'image/png' },
    ],
    shortcut: '/Gemini_Generated_Image_wai7uiwai7uiwai7-removebg-preview.png',
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <Analytics /> 
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
