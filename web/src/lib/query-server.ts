const server: string = 'http://10.100.148.175:8080';

export async function add_relationship(
	person1: string,
	code: string,
	relationship: 'best_friends' | 'friends' | 'family' | 'married' | 'romantic' | 'work',
	context: string
): Promise<any> {
	try {
		const response = await fetch(server + '/add-connection', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: person1 + ' ' + code + ' ' + relationship + ' ' + context
		});

		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}

		const result = await response.json();
		return result;
	} catch (error) {
		throw error;
	}
}
export async function create_user(
	username: string
): Promise<{ error: string } | { message: string }> {
	try {
		const response = await fetch(server + '/create-user', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: username
		});
		console.log('the fetch has been confirmed');

		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}

		const result = await response.json();
		console.log(result);
		return result;
	} catch (error) {
		return { error: error as string };
	}
}
export async function update_private_bio(person: string, personal_bio: string): Promise<any> {
	try {
		const response = await fetch(server + '/update-private-bio', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: person + ' ' + personal_bio
		});

		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}

		const result = await response.json();
		return result;
	} catch (error) {
		throw error;
	}
}
export async function update_public_bio(person: string, public_bio: string): Promise<any> {
	try {
		const response = await fetch(server + '/update-public-bio', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: person + ' ' + public_bio
		});

		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}

		const result = await response.json();
		return result;
	} catch (error) {
		throw error;
	}
}

async function fetch_server(url: string): Promise<any> {
	try {
		const response = await fetch(url);
		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}
		return response.json();
	} catch (error) {
		return { error: error as string };
	}
}

export async function get_relationships(person: string): Promise<any> {
	return fetch_server(server + '/get-relationships?name=' + encodeURIComponent(person));
}
export async function get_person(person: string): Promise<any> {
	return fetch_server(server + '/get-person?name=' + encodeURIComponent(person));
}
export async function get_user_code(person: string): Promise<{ friendCode: string }> {
	return fetch_server(server + '/get-user-code?name=' + encodeURIComponent(person));
}
export function username_exists(username: string): Promise<{ found: boolean }> {
	return fetch_server(server + '/username-found?name=' + encodeURIComponent(username));
}
export async function find_user_match(searcher: string, filter: string): Promise<any> {
	console.log(
		server +
			'/search-people?filter=' +
			encodeURIComponent(filter) +
			'&searcher=' +
			encodeURIComponent(searcher)
	);
	return fetch_server(
		server +
			'/search-people?filter=' +
			encodeURIComponent(filter) +
			'&searcher=' +
			encodeURIComponent(searcher)
	);
}
