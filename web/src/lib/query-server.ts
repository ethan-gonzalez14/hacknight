const server: string = 'http://localhost:8080';

export async function add_relationship(person1: string, person2: string): Promise<any> {
	try {
		const response = await fetch(server + '/add-connection', {
			method: 'POST',
			headers: {
				'Content-Type': 'text/plain'
			},
			body: person1 + ' ' + person2
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
export async function get_relationships(person: string): Promise<any> {
	try {
		const response = await fetch(server + '/get-relationships?name=' + person);

		if (!response.ok) {
			throw new Error(`HTTP error status: ${response.status}`);
		}

		const result = await response.json();
		return result;
	} catch (error) {
		throw error;
	}
}
