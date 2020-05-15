import React, { Component } from 'react';
import { Router , Route, Switch, Redirect } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import styled from '@emotion/styled';
import EnterSecret from '../pages/EnterSecret'
import RenderSecretUrl from '../pages/RenderSecretUrl'

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: auto;
  width: auto;
  position: relative;
`;
export const history = createBrowserHistory();

class Routes extends Component {

	render() {
		return (
			<Router history={history}>
				<Container>
					<Switch>
						<Route exact path='/' component={EnterSecret} />
                        <Route exact path='/success_creation' component={RenderSecretUrl} />
						<Redirect from='*' to='/' />
					</Switch>
				</Container>
			</Router>
		);
	}
}

export default Routes;
