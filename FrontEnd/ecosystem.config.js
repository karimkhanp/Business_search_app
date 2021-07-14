module.exports = {
  apps: [
    {
      exec_mode: 'cluster',
      name: 'testingFE1',
      cwd: '/home/ubuntu/Test-dir/Business_search_app/FrontEnd',
      script: './node_modules/nuxt/bin/nuxt.js',
      host: '0.0.0.0',
      port: 3030,
      instances: 'max',
      args: 'stremotart'
    },

  ]
};
