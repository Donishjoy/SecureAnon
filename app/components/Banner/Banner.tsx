import Image from "next/image";



const Banner = () => {
    return (
        <main>
            <div className="px-6 lg:px-8">
                <div className="mx-auto max-w-7xl pt-16 sm:pt-20 pb-20 banner-image">
                    <div className="text-center">
                        <h1 className="text-4xl font-semibold text-navyblue sm:text-5xl  lg:text-7xl md:4px lh-96">
                        Protect Privacy and Ensure Compliance <br />with SecurAnon.
                        </h1>
                        <p className="mt-6 text-lg leading-8 text-bluegray">
                        SecurAnon is an easy-to-use online tool designed to safeguard privacy and adhere<br /> to regulations by anonymizing images and videos.
                        </p>
                    </div>


                </div>
            </div>
        </main>
    )
}

export default Banner;
