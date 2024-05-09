'use client'
import { Dialog, Transition } from '@headlessui/react'
import { Fragment, useState } from 'react'
import { LockClosedIcon } from '@heroicons/react/20/solid'
import { useRouter } from 'next/navigation'
import { ClimbingBoxLoader } from 'react-spinners'
export default function Register() {
    let[loading,setLoading]=useState(false)
    let [isOpen, setIsOpen] = useState(true)
    let[isVerify,setVerify]=useState(false)
    const [email, setEmail] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [msg,setMsg]=useState<string>('');
    const [otp, setotp] = useState<string>('');
    const handleEmail = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setEmail(event.target.value);
    }

    const router=useRouter();
    const handlePassword = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    }
    const handleOtp = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setotp(event.target.value);
    }

    const checkPasswordStrength = (password: string) => {
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(password);
        const isLongEnough = password.length >= 6;
    
        return hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar && isLongEnough;
      };   

    const handleSubmit = async () => {
        if (!checkPasswordStrength(password)) {
            setMsg('Password is weak. Please use a combination of uppercase, lowercase, numbers, and special characters.');
            return;
          }else{
        console.log(email, password);
        const formdata = new FormData();
        formdata.append('email', email);
      
        setLoading(true);
        setIsOpen(false);
        setVerify(false);
        const response = await fetch('http://127.0.0.1:5000/api/register', {
            method: 'POST',
            body: formdata,
        });

        if (response.ok) {
            setLoading(false);
            const data = await response.json();
            console.log(data.msg);
            console.log(data.status_code);
            
            
            if(data.status_code==201){
                setIsOpen(false);
                setVerify(true);
            }
             
        }
    }
    }

    const handleVerify = async () => {

        console.log(email, otp);
        const formdata = new FormData();
        formdata.append('email', email);
        formdata.append('otp', otp);
        formdata.append('password', password);
        const response = await fetch('http://127.0.0.1:5000/api/verify', {
            method: 'POST',
            body: formdata,
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            console.log(data.msg);
            console.log(data.status_code);
            setMsg(data.msg);
            
            if(data.status_code==201){
                setIsOpen(false);
                setVerify(false);
                router.push('/Signin');
            }
             
        
    }else{
        setMsg("Invalid OTP");
    }
    }
    const closeModal = () => {
        setIsOpen(false)
    }

    const openModal = () => {
        setIsOpen(true)
    }

    return (
        <>
        <ClimbingBoxLoader
  color="#21ba04"
  size={25}
  speedMultiplier={1}
  loading={loading}
  style={{marginTop:'50%',marginRight:'50%',marginBottom:'50%', marginLeft:'50%'}}
/>

            <Transition appear show={isVerify} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={closeModal}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>
                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">

                                    <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                                        <div className="w-full max-w-md space-y-8">
                                            <div>
                                                <img
                                                    className="mx-auto h-12 w-auto"
                                                    src="/assets/logo/l1.svg"
                                                    alt="Company"
                                                />
                                                <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                                                    OTP Verification
                                                </h2>
                                            </div>
                                            <form className="mt-8 space-y-6" method="POST">
                                                <input type="hidden" name="remember" defaultValue="true" />
                                                <div className="-space-y-px rounded-md shadow-sm">
                                                    <div>
                                                        <label htmlFor="email-address" className="sr-only">
                                                            OTP
                                                        </label>
                                                        <input
                                                            id="email-address"
                                                            name="otp"
                                                            type="text"
                                                            required
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="Enter OTP"
                                                            onChange={handleOtp}
                                                        />
                                                    </div>
                                                    
                                                </div>


                                                <div>
                                                    <button
                                                        type="submit"
                                                        className="group relative flex w-full justify-center rounded-md border border-transparent bg-blue py-2 px-4 text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                                        onClick={handleVerify} >
                                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                                            <LockClosedIcon className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                                                        </span>
                                                        Verify Now
                                                    </button>
                                                </div>
                                                <div ><center><h3  className='text-danger'>{msg}</h3></center> 
                                                </div>
                                            </form>
                                        </div>
                                    </div>


                                    <div className="mt-4 flex justify-end">

                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
            <Transition appear show={isOpen} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={closeModal}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">

                                    <div className="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
                                        <div className="w-full max-w-md space-y-8">
                                            <div>
                                                <img
                                                    className="mx-auto h-12 w-auto"
                                                    src="/assets/logo/l1.svg"
                                                    alt="Your Company"
                                                />
                                                <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
                                                    Register your account
                                                </h2>
                                            </div>
                                            <form className="mt-8 space-y-6" action="#" method="POST">
                                                <input type="hidden" name="remember" defaultValue="true" />
                                                <div className="-space-y-px rounded-md shadow-sm">
                                                    <div>
                                                        <label htmlFor="email-address" className="sr-only">
                                                            Email address
                                                        </label>
                                                        <input
                                                            id="email-address"
                                                            name="email"
                                                            type="email"
                                                            autoComplete="email"
                                                            required
                                                            className="relative block w-full appearance-none rounded-none rounded-t-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="Email address"
                                                            onChange={handleEmail}
                                                        />
                                                    </div>
                                                    <br>
                                                    </br>

                                                    <div>
                                                        <label htmlFor="password" className="sr-only">
                                                            Password
                                                        </label>
                                                        <input
                                                            id="password"
                                                            name="password"
                                                            type="password"
                                                            autoComplete="current-password"
                                                            required
                                                            className="relative block w-full appearance-none rounded-none rounded-b-md border border-grey500 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                                                            placeholder="Password"
                                                            onChange={handlePassword}
                                                            minLength={6}
                                                        />
                                                    </div>
                                                </div>

                                                <div className="flex items-center justify-between">
                                                    <div className="flex items-center">
                                                        <a href='/Signin'>
                                                            <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                                                                Already Registered
                                                            </label>
                                                        </a>
                                                    </div>

                                                </div>

                                                <div>
                                                    <button
                                                        type="submit"
                                                        className="group relative flex w-full justify-center rounded-md border border-transparent bg-blue py-2 px-4 text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                                                        onClick={handleSubmit}
                                                    >
                                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3">
                                                            <LockClosedIcon className="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" aria-hidden="true" />
                                                        </span>
                                                        Register Now
                                                    </button>
                                                </div>
                                                <div ><center><h3  className='text-danger'>{msg}</h3></center> 
                                                </div>
                                            </form>
                                        </div>
                                    </div>



                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </>
    )
}

