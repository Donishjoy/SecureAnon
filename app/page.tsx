'use client'
import Signin from '../components/Navbar/Signdialog';
import { useRouter } from 'next/navigation';

export default function Home({ token }: { token?: string }) {
  const router = useRouter();

  if (token) {
    console.log(token);
    router.push('/dashboard');
  }

  return (
    <main>
      <Signin />
    </main>
  );
}