'use client'
import Banner from "@/components/Banner/Banner"
import Provide from "@/components/Provide"
import Why from "@/components/Why"
import { useRouter } from "next/navigation"
export default function Home() {
    const router = useRouter();
    
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token');

        if (!token) {
            router.push('/Signin');
        }
        console.log("dashboard", token);
    }
    
    return (
        <main>
            <Banner />
            <Provide />
            <Why />
        </main>
    )
}
