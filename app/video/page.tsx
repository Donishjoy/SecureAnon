'use client'
import React, { useState } from 'react';
import { ClimbingBoxLoader } from 'react-spinners';
import { useRouter } from 'next/navigation';
import { ToastContainer,toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
export default function FileUpload() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const [VideoUrl, setUploadedVideoUrl] = useState<string>('');
    const [videoId,setVideoId]=useState<string>('');
    const [video_path,setVideoPath] = useState<string>('');
    let[loading,setLoading]=useState(false);   
    let[background,setBackground]=useState(false);

const router=useRouter();

const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const File = event.target.files[0];
      if (File.type.startsWith('video/')) {
        setSelectedFile(File);
      } else {
        toast.error('⚠️ Please select a video file', {
          position: 'top-right',
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: 'colored',
        });
      }
    }
  };

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const selectedImage = event.target.files[0];
      if (selectedImage.type.startsWith('image/')) {
        setSelectedImage(selectedImage);
      } else {
        toast.error('⚠️ Please select an image file', {
          position: 'top-right',
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: 'colored',
        });
      }
    }
  };

    const handleSubmit = async () => {
        if (!selectedFile) {
            toast.error('⚠️ Please select a file', {
                position:"top-right",
                autoClose: 5000,
                hideProgressBar: true,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "colored",
                
                });
            return;
        }
        
        const token=localStorage.getItem('token');
        if(!token){
            router.push('/Signin');
        }
        const formData = new FormData();
        formData.append('file', selectedFile);
        setBackground(true);
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/api/videoupload', {
                method: 'POST',
                body: formData,
                headers:{
                    'Authorization':`Bearer ${token}`
                }
            });

            if (response.ok) {
                const data=await response.json();
                console.log("data",data); 
                setVideoId(data.video_id);
                setVideoPath(data.file_path);
                setLoading(false);
                setBackground(false);
                
            } else {
                console.error('Failed to process file');
            }
        } catch (error) {
            console.error('Error processing file:', error);
        }
    };


    const handleprocess = async () => {
        console.log("selected Image", selectedImage);
        if (!selectedImage) {
            toast.error('⚠️ Please select a file', {
                position:"top-right",
                autoClose: 5000,
                hideProgressBar: true,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                theme: "colored",
                
                });
            return;
        }
        console.log("videoid and path", video_path, videoId);
        console.log("selected Image", selectedImage);
        // Create a new FormData object
        const formData = new FormData();
        formData.append('file', selectedImage);
        formData.append('video_path', video_path);
        formData.append('video_id', videoId);
        const token=localStorage.getItem('token');
        if(!token){
            router.push('/Signin');
        }
        setLoading(true);
        try {
            const response = await fetch('http://127.0.0.1:5000/api/reference', {
                method: 'POST',
                body: formData,
                headers:{
                    'Authorization':`Bearer ${token}`
                }
            });
    
            if (response.ok) {
                const data=await response.json();
                console.log('success',data.output);

                setUploadedVideoUrl(data.output);
                setLoading(false);
            } else {
                console.error('Failed to process file');
            }
        } catch (error) {
            console.error('Error processing file:', error);
        }
    };
    

    const handleDownload = async () => {
        
        if (VideoUrl) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/${VideoUrl}`);
                console.log("successful",response);
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
    
                // Create a temporary link element
                const link = document.createElement('a');
                link.href = url;
                link.download = 'processed_video.mp4'; // Set the desired file name
                document.body.appendChild(link);
    
                // Programmatically click the link to trigger the download
                link.click();
    
                // Clean up by removing the link and revoking the URL object
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
            } catch (error) {
                console.error('Error downloading image:', error);
            }
        }
    };
    

    return (
        
        <div style={{ backgroundColor: 'white', padding: '20px', maxWidth: '60%', margin: 'auto', alignContent: 'center', overflowY: 'auto',scrollBehavior:'smooth',marginBottom:'10%' }}>
            <br />
            <ClimbingBoxLoader
  color="#21ba04"
  size={25}
  speedMultiplier={1}
  loading={loading}
  style={{marginTop:'50%',marginRight:'50%',marginBottom:'50%', marginLeft:'50%'}}
/>
<ToastContainer
position="top-right"
autoClose={5000}
hideProgressBar={false}
newestOnTop={false}
closeOnClick
rtl={false}
pauseOnFocusLoss
draggable
pauseOnHover
theme="light"
/>
{/* Same as */}
<ToastContainer />
<div hidden={background}>
            <div className="col-span-full" >
                <label htmlFor="file-upload" >Upload Video</label>
                <br />
                <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                    <div className="text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clipRule="evenodd" />
                        </svg>
                        <div className="mt-4 flex text-sm leading-6 text-gray-600">
                            <label htmlFor="file-upload" className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
                                <span>Upload a video file</span>
                                <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileUpload} />
                            </label>
                         
                        </div>
                        <p className="text-xs leading-5 text-gray-600">MP4</p>
                    </div>
                </div>
            </div>
            <br />

            <button  type="button" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={handleSubmit} style={{marginLeft:"40%"}}>Upload Video</button>
            <br />
            <br/>
            <div className="col-span-full">
                <label htmlFor="image-upload" >Upload Reference Image</label>
                <br />
                <br/>
                <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                    <div className="text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clipRule="evenodd" />
                        </svg>
                        <div className="mt-4 flex text-sm leading-6 text-gray-600">
                            <label htmlFor="image-upload" className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
                                <span>Upload an image file</span>
                                <input id="image-upload" name="image-upload" type="file"  className="sr-only" onChange={handleImageUpload} />
                            </label>
          
                        </div>
                        <p className="text-xs leading-5 text-gray-600">PNG , JPEG</p>
                    </div>
                </div>
            </div>
            <br />

            {selectedFile && selectedImage && (<button type="button" className="bg-success hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={handleprocess} style={{marginLeft:"80%"}}>Process Video</button>)}

            {VideoUrl && (
                <div>
                    <video src="https://www.youtube.com/watch?v=GXcy7Di1oys&list=PLUE9cBml08yi4OVpg4tR7yGBGgJjyfi3y"  style={{ marginTop: '10px', width: '50%', height: '30%' }} />

                    <br />
                    <button type="button" className="bg-warning hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={handleDownload}>Download Processed Video</button>
                </div>
                
            )}
            <div>
                <br/>

            </div>
            </div>
        </div>
    );
}
