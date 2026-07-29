module.exports={
    webpackdevmiddleware: config => {
        config.watchOptions.poll = 300;
        return config;
    },
     allowedDevOrigins: ['ticketing.dev'],
}