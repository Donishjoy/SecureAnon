'use client'
import React, { useState } from 'react';
export default function FileUpload() {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [uploadedImageUrl, setUploadedImageUrl] = useState<string>('');
    const [blurFactor, setBlurFactor] = useState<number>(3); // Default blur factor


    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleSubmit = async () => {
        if (!selectedFile) {
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('blur_factor', blurFactor.toString()); // Convert to string

        try {
            const response = await fetch('http://127.0.0.1:5000/api/file', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
              
                setUploadedImageUrl(data.output_path);
                console.log(uploadedImageUrl);
            } else {
                console.error('Failed to process file');
            }
        } catch (error) {
            console.error('Error processing file:', error);
        }
    };

    const handleBlurFactorChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setBlurFactor(parseInt(event.target.value));
    };
    const handleDownload = async () => {
        
        if (uploadedImageUrl) {
            try {
                const response = await fetch(`http://127.0.0.1:5000/${uploadedImageUrl}`);
                console.log("successful",response);
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
    
                // Create a temporary link element
                const link = document.createElement('a');
                link.href = url;
                link.download = 'processed_image.jpg'; // Set the desired file name
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
            <div className="col-span-full">
                <label htmlFor="file-upload" >Upload Image</label>
                <br />
                <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                    <div className="text-center">
                        <svg className="mx-auto h-12 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                            <path fillRule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clipRule="evenodd" />
                        </svg>
                        <div className="mt-4 flex text-sm leading-6 text-gray-600">
                            <label htmlFor="file-upload" className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500">
                                <span>Upload a file</span>
                                <input id="file-upload" name="file-upload" type="file" className="sr-only" onChange={handleFileUpload} />
                            </label>
                            <p className="pl-1">or drag and drop</p>
                        </div>
                        <p className="text-xs leading-5 text-gray-600">PNG, JPG</p>
                    </div>
                </div>
            </div>
            <br />
            <label htmlFor="blur-factor" className="block text-sm font-bold leading-6 text-gray-900">Blur Factor</label>
            <input id="blur-factor" name="blur-factor" type="number" min="1" max="5" value={blurFactor.toString()} onChange={handleBlurFactorChange} />
            <br />
            <button type="button" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={handleSubmit}>Process Image</button>
            <br />
            {uploadedImageUrl && (
                <div>
                    <img src={`http://127.0.0.1:5000/${uploadedImageUrl}`} alt="Processed" style={{ marginTop: '10px', width: '50%', height: '30%' }} />

                    <br />
                    <button type="button" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={handleDownload}>Download Processed Image</button>
                </div>
                
            )}
            <div>
                <br/>
                
            </div>
        </div>
    );
}
