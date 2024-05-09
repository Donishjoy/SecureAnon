'use client'
import { Dialog, Transition } from '@headlessui/react'
import { Fragment, use, useState } from 'react'
import { LockClosedIcon } from '@heroicons/react/20/solid'
import { useRouter } from 'next/navigation'
import { ClimbingBoxLoader } from 'react-spinners'
export default function Verify() {
    let [isOpen, setIsOpen] = useState(true)
    let[loading,setLoading]=useState(false)
    const [otp, setotp] = useState<string>('');
    const [msg,setMsg]=useState<string>('');
    const closeModal = () => {
        setIsOpen(false);
    };

console.log(localStorage.getItem('email'));
    const handleOtp = async (event: React.ChangeEvent<HTMLInputElement>) => {
        setotp(event.target.value);
    }
    const router = useRouter();
   
    const handleSubmit = async () => {
        console.log(otp);
        const formdata = new FormData();
        if(otp){
            console.log("otp",otp);
            
            setMsg('Please enter OTP');
            setIsOpen(true)
        }else{
            formdata.append('otp', otp);
            setIsOpen(false);
            setLoading(true);
            const response = await fetch('http://127.0.0.1:5000/api/verify', {
                method: 'POST',
                body: formdata
            });
    
            if (response.ok) {
                const data = await response.json();
                console.log(data.msg, data.token);
                setMsg(data.msg)
                if(data.token){
                    
                    localStorage.setItem('token', data.token);
                    setLoading(false);
                    router.push('/dashboard');
    
                }
                else{
                    setIsOpen(true);
                }
        }
 
        }

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
                                                        onClick={handleSubmit} >
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
        </>
    )
}

