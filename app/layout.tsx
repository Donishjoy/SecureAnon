import './globals.css';
import Navbar from '@/components/Navbar/Navbar';

export const metadata = {
  title: 'SecureAnon',
  description: '',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <div style={{marginTop:"10%"}}></div>
        {children}
        {/* <Footer /> */}
      </body>
    </html>
  )
}
