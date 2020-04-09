import React from 'react'
import { Route, Switch } from 'react-router-dom'

import { socketIO } from '../../../func/sockets'

import './style.css'

import Posts from '../../Posts'
import Post from '../../Post'


export default class App extends React.Component {
	componentWillMount() {
		const token = localStorage.getItem('token')

		// Online

		socketIO.on('connect', () => {
			socketIO.emit('online', {token})
		})

		socketIO.on('online_add', (x) => {
			console.log('ADD', x)
			this.props.onlineAdd(x)
		})

		socketIO.on('online_del', (x) => {
			console.log('DEL', x)
			this.props.onlineDelete(x)
		})

		socketIO.on('disconnect', () => {
			this.props.onlineReset();
		})
	}

	render() {
		const { online } = this.props

		if (!online.count) {
			return (
				<>
					Loading..
				</>
			)
		}

		return (
			<div className="container" id="main">
				<Switch>
					<Route exact path="/">
						<Posts />
					</Route>

					<Route path="/posts">
						<Posts />
					</Route>
					<Route path="/post">
						<Post />
					</Route>
				</Switch>
			</div>
		)
	}
}