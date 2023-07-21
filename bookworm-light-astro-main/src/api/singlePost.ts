import server_url from "@config/serverUrl.json"

export interface Meta {
    total_count: number;
}

export interface MetaDetail {
    type: string;
    detail_url: string;
    html_url: string;
    slug: string;
    first_published_at: string;
}

export interface BodyContent {
    type: "content";
    value: string;
    id: string;
}

export interface BodyImage {
    type: "image";
    value: {
        image_url: string;
        caption: string;
    };
    id: string;
}

type Body = (BodyContent | BodyImage)[];

interface Item {
    id: number;
    meta: MetaDetail;
    title: string;
    date_post: string;
    description: string;
    body: Body;
    categories: { name: string }[];
    author: string;
}

export interface ResponseData {
    meta: Meta;
    items: Item[];
}

export const fetchSinglePost = async(slug: any): Promise<ResponseData> => {
    const response = await fetch(`${server_url.server}${server_url.listPosts}?type=blog.BlogPage&slug=${slug}&fields=description,date_post,body,categories(id,name),author`);
    const data = await response.json();
    return data;
}