import server_url from "@config/serverUrl.json"
export interface PostsList {
    meta: {
        total_count: number
    };
    items: BlogPost[];
}

export interface BlogPost {
    id: number;
    meta: {
        type: string;
        detail_url: string;
        html_url: string;
        slug: string;
        first_published_at: string;
    };
    title: string;
    date_post: string;
    description: string;
    feed_image: FeedImage;
    categories: Category[];
    author: string;
}

// Interface for the Feed Image
export interface FeedImage {
    id: number;
    meta: {
        type: string;
        detail_url: string;
        download_url: string;
    };
    title: string;
}

// Interface for the Category
export interface Category {
    name: string;
}

const toJson = (res: Response) => {
    if (res.status === 404) {
        return undefined;
    }

    return res.json();
};

export const fetchPostsList = async (type?: string, fields?: string, order?: string): Promise<PostsList> => {
    const response = await fetch(`${server_url.server}${server_url.listPosts}?type=${type}&fields=${fields}&order=${order}`);
    const data = await response.json();
    return data;
};

export const fetchFilterCategories = async (type?: string, fields?: string, order?: string, limit?:number, categoriesid?: number ): Promise<PostsList> =>{
    const response = await fetch(`${server_url.server}${server_url.listPosts}?type=${type}&fields=${fields}&order=${order}&limit=${limit}&categories=${categoriesid}`);
    const data = await response.json();
    return data;
}