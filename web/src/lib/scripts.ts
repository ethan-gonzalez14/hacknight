export function add_connection(username: string, code: string) {
	return new Promise((resolve, reject) => {
		fetch('/api/add_connection', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, code })
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then((data) => resolve(data))
			.catch((error) => reject(error));
	});
}
