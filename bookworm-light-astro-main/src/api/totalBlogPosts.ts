import server_url from "@config/serverUrl.json"

export interface TotalBlogs{
    total_posts: number;
}

export const fetchTotalBlogs = async(): Promise<TotalBlogs> => {
    const response = await fetch(`${server_url.server}${server_url.totalBlogs}`);
    const data = await response.json();
    return data;
}