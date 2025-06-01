const server: string = 'http://localhost:8080';

export async function add_relationship(person1: string, code: string): Promise<any> {
	try {
		const response = await fetch(server + '/add-connection', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: person1 + ' ' + code
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
		return { error };
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
		throw error;
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
