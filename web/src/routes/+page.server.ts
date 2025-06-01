import type { PageServerLoad } from './$types';
import { create_user, username_exists } from '$lib/query-server'; // Adjust path as needed
import { redirect, type Actions } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies }) => {
	const username = cookies.get('username');
	console.log(username);

	return {
		loggedIn: username !== undefined,
		username
	};
};

export const actions: Actions = {
	login: async ({ request, cookies }) => {
		const data = await request.formData();
		const username = data.get('username')?.toString();

		if (!username) return { error: 'USERNAME_NOT_GIVEN' };

		const exists = (await username_exists(username)).found;
		if (exists) {
			cookies.set('username', username, { path: '/' });
			return redirect(302, '/');
		} else {
			return { error: 'USER_NOT_FOUND' };
		}
	},

	register: async ({ request, cookies }) => {
		const data = await request.formData();
		const username = data.get('username')?.toString();

		console.log('Registering user:', username);

		if (!username) return { error: 'USERNAME_NOT_GIVEN' };

		const available = !('error' in (await create_user(username)));
		console.log('Username available:', available);

		if (!available) return { error: 'USERNAME_NOT_AVAILABLE' };
		cookies.set('username', username, { path: '/' });

		// Your registration logic here (e.g. create user)
		// Assume register succeeded for demo:
		return redirect(302, '/');
	},

	logout: async ({ cookies }) => {
		console.log('logging out');
		cookies.delete('username', { path: '/' });
		return redirect(302, '/');
	}
};
