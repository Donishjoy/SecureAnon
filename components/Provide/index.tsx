// components/Provide/index.tsx

import Image from "next/image";
import Link from "next/link";
import type { FC } from "react";

interface DataType {
    imgSrc: string;
    country: string;
    paragraph: string;
    button: string;
    link: string;
}

const AboutData: DataType[] = [
    {
        imgSrc: "/assets/provide/image.svg",
        country: "Auto Image Anonymization",
        paragraph: 'Automatically blur faces in images for enhanced privacy protection.',
        button: "Try It Now",
        link: "image"
    },
    {
        imgSrc: "/assets/provide/face.svg",
        country: "Selective Image Anonymization",
        paragraph: 'Selective face anonymization to safeguard privacy effectively.',
        button: "Try It Now",
        link: "selective"
    },
    {
        imgSrc: "/assets/provide/video.svg",
        country: "Video Anonymization",
        paragraph: 'Anonymize faces, text, and watermarks in videos to safeguard individuals identities.',
        button: "Try It Now",
        link: "video"
    },
];

const Provide: FC = () => {
    return (
        <div id="services">
            <div className='mx-auto max-w-7xl px-4 my-10 sm:py-20 lg:px-8'>
                <div className='grid grid-cols-1 lg:grid-cols-12 gap-8'>
                    {/* COLUMN-1 */}
                    <div className='col-span-6 flex justify-center'>
                        <div className="flex flex-col align-middle justify-center p-10">
                            <p className="text-4xl lg:text-6xl pt-4 font-semibold lh-81 mt-5 text-center lg:text-start">We provide that service.</p>
                            <h4 className="text-lg pt-4 font-normal lh-33 text-center lg:text-start text-bluegray">SecurAnon simplifies the process of safeguarding privacy in both images and videos. With its intuitive interface and powerful features, users can detect and blur faces, remove watermarks, and ensure compliance with privacy regulations, all while retaining full control over their media content.</h4>
                        </div>
                    </div>
                    <div className='lg:col-span-1'></div>
                    {/* COLUMN-2 */}
                    <div className='col-span-6 lg:col-span-5'>
                        <div className='grid grid-cols-1 sm:grid-cols-2 gap-x-16 gap-y-10 lg:gap-x-40 px-10 py-12 bg-bluebg rounded-3xl'>
                            {AboutData.map((item, i) => (
                                <div key={i} className='bg-white rounded-3xl lg:-ml-32 p-6 shadow-xl'>
                                    <Image src={item.imgSrc} alt={item.imgSrc} width={64} height={64} className="mb-5" />
                                    <h4 className="text-2xl font-semibold">{item.country}</h4>
                                    <h4 className='text-lg font-normal text-bluegray my-2'>{item.paragraph}</h4>
                                    <Link href={`/${item.link}`} passHref>
                                        <button type="button" className="mt-4 text-xl font-medium text-blue flex gap-2 mx-auto lg:mx-0 space-links">{item.button}</button>
                                    </Link>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Provide;
