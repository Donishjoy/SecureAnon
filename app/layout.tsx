import './globals.css';
import Navbar from './components/Navbar/index';



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
        {children}
        {/* <Footer /> */}
      </body>
    </html>
  )
}
