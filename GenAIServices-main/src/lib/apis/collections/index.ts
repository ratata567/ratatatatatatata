import { WEBUI_API_BASE_URL } from '$lib/constants';

export const createNewColleciton = async (
	token: string,
	collection_name: string) => {
	let error = null;
	// console.log("Here")
	// console.log(title)
	// console.log(vector_ids)
	const searchParams = new URLSearchParams();
	searchParams.append('collection_name', collection_name);

	const res = await fetch(`${WEBUI_API_BASE_URL}/collections/create?${searchParams.toString()}`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			collection_name: collection_name
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const getCollections = async (token: string = '') => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/collections/`, {
		method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;
			console.log(err);
			return null;
		});
	console.log(res)
	if (error) {
		console.log(res)
		throw error;
	}

	return res;
};

export const deleteCollectionByName = async (token: string, collection_name: string) => {
	let error = null;

	const searchParams = new URLSearchParams();
	searchParams.append('collection_name', collection_name);

	const res = await fetch(`${WEBUI_API_BASE_URL}/collections/collection/delete?${searchParams.toString()}`, {
		method: 'DELETE',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.then((json) => {
			return json;
		})
		.catch((err) => {
			error = err.detail;

			console.log(err);
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};