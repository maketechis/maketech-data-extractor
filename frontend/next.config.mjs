/** @type {import('next').NextConfig} */
const desktop=process.env.NEXT_PUBLIC_DESKTOP==="1";
const nextConfig=desktop?{output:"export",images:{unoptimized:true},trailingSlash:true}:{};
export default nextConfig;
