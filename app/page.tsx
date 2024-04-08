'use client'
import Signin from '../components/Navbar/Signdialog';
import { useRouter } from 'next/navigation';
export default function Home() {
  const token=localStorage.getItem('token');
  const router=useRouter();
   if (token) {
    console.log(token);
router.push('/dashboard');
   }
  return (
    <main>
<Signin/>
    </main>
  )
}
