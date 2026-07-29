import 'bootstrap/dist/css/bootstrap.css';
import buildClient from '../api/build-client';
import Header from '../components/header';

function AppComponent({ Component, pageProps, currentUser }) {
  return (
    <div>
      <Header currentUser={currentUser} />
      <div className="container">
      <Component currentUser={currentUser} {...pageProps} />
      </div>
    </div>
  );
}

AppComponent.getInitialProps = async (appContext) => {
  let currentUser = null;
  let client;
  try {
     client= await buildClient(appContext.ctx)
     let clientData=await client.get('/api/users/currentUser');
    currentUser = clientData.data.currentUser;
  } catch (err) {
    // Treat 401/404 as unauthenticated and otherwise rethrow.
    if (!(err.response && [401, 404].includes(err.response.status))) {
      throw err;
    }
  }

  const { Component, ctx } = appContext;
  let pageProps = {};
  if (Component.getInitialProps) {
    pageProps = await Component.getInitialProps(ctx,client, currentUser);
  }

  return { pageProps, currentUser };
};

export default AppComponent;