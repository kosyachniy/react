import i18n from './i18n'

import { combineReducers, createStore } from 'redux';


// actions.js
export const postsGet = posts => ({
	type: 'POSTS_GET',
	posts,
});

export const postsAdd = note => ({
	type: 'POSTS_ADD',
	note,
});

export const postsDelete = id => ({
	type: 'POSTS_DELETE',
	id,
});

export const onlineAdd = online => ({
	type: 'ONLINE_ADD',
	count: online.count,
	users: online.users,
});

export const onlineDelete = online => ({
	type: 'ONLINE_DELETE',
	count: online.count,
	ids: online.users.map(user => user.id),
});

export const onlineReset = () => ({
	type: 'ONLINE_RESET',
});

export const changeTheme = theme => {
	localStorage.setItem('theme', theme)

	const color = theme === 'dark' ? 'light' : 'dark'
	localStorage.setItem('color', color)

	return {
		type: 'CHANGE_THEME',
		theme, color,
	}
}

export const changeLang = lang => {
	localStorage.setItem('lang', lang)
	i18n.changeLanguage(lang)

	return {
		type: 'CHANGE_LANG',
		lang,
	}
}

export const profileIn = profile => {
	const { id, login, name, avatar, admin } = profile

	localStorage.setItem('id', id)
	localStorage.setItem('login', login)
	localStorage.setItem('name', name)
	localStorage.setItem('avatar', avatar)
	localStorage.setItem('admin', admin)

	return {
		type: 'PROFILE_IN',
		id, login, name, avatar, admin,
	}
};

export const peofileOut = () => {
	localStorage.removeItem('id')
	localStorage.removeItem('login')
	localStorage.removeItem('name')
	localStorage.removeItem('avatar')
	localStorage.removeItem('admin')

	return {
		type: 'PROFILE_OUT',
	}
};

export const systemLoaded = () => ({
	type: 'SYSTEM_LOADED',
});

// reducers.js
export const posts = (state = [], action) => {
	switch (action.type) {
		case 'POSTS_GET':
			return action.posts;

		case 'POSTS_ADD':
			return [
				action.note,
				...state
			];

		case 'POSTS_DELETE':
			return state.filter(note => note.id !== action.id);

		default:
			return state;
	}
};

export const online = (state = {count: null, users: []}, action) => {
	switch (action.type) {
		case 'ONLINE_ADD':
			return {
				count: action.count,
				users: [
					...action.users,
					...state.users
				]
			};

		case 'ONLINE_DELETE':
			return {
				count: action.count,
				users: state.users.filter(user => action.ids.indexOf(user.id) === -1),
			};

		case 'ONLINE_RESET':
			return {count: null, users: []};

		default:
			return state;
	}
};

export const system = (state = {
	loaded: false,
	lang: localStorage.getItem('lang'),
	theme: localStorage.getItem('theme'),
	color: localStorage.getItem('color'),
}, action) => {
	switch (action.type) {
		case 'CHANGE_THEME':
			return {
				...state,
				theme: action.theme,
				color: action.color,
			};

		case 'CHANGE_LANG':
			return {
				...state,
				lang: action.lang,
			};

		case 'SYSTEM_LOADED':
			return {
				...state,
				loaded: true,
			};

		default:
			return {
				loaded: state.loaded,
				lang: state.lang || 'ru',
				theme: state.theme || 'light',
				color: state.color || 'dark',
			};
	}
};

export const profile = (state = {id: 0, login: null, name: null, avatar: null, admin: 2}, action) => {
	switch (action.type) {
		case 'PROFILE_IN':
			return {
				id: action.id,
				login: action.login,
				name: action.name,
				avatar: action.avatar,
				admin: action.admin,
			};

		case 'PROFILE_OUT':
			return {
				id: 0,
				login: null,
				name: null,
				avatar: null,
				admin: 2,
			};

		default:
			return {
				id: state.id || localStorage.getItem('id'),
				login: state.login || localStorage.getItem('login'),
				name: state.name || localStorage.getItem('name'),
				avatar: state.avatar || localStorage.getItem('avatar'),
				admin: state.admin || localStorage.getItem('admin'),
			};
	}
};

export const reducers = combineReducers({
	system, online, profile, posts,
});

// store.js
export function configureStore(initialState = {}) {
	const store = createStore(reducers, initialState);
	return store;
}

export const store = configureStore();