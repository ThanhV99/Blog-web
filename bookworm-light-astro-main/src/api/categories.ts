import server_url from "@config/serverUrl.json"
export interface Category {
    id: number;
    slug: string;
    name: string;
}

export interface CategoryApiResponse {
    meta: {
        total_count: number;
    };
    items: Category[];
}

export const fetchCategoriesList = async (): Promise<CategoryApiResponse> => {
    const response = await fetch(`${server_url.server}${server_url.listCategories}`);
    const data = await response.json();
    return data;
};