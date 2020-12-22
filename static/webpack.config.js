const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");

module.exports = {
  entry: {
    app: "./src/js/index.js",
  },
  mode: "development",
  watch: true,
  devtool: "source-map",
  output: {
    filename: "[name].bundle.js",
    path: path.resolve(__dirname, "dist"),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.s[ac]ss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          // "style-loader",
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif|ico)$/i,
        loader: "file-loader",
        options: {
          name: "[name].[ext]",
          // publicPath: '../dist/media',
          publicPath: "../../media",
          outputPath: "/media",
        },
      },
      {
        test: /\.(woff|woff2|otf|ttf|eot|svg)$/i,
        loader: "file-loader",
        options: {
          name: "[name].[ext]",
          publicPath: "../dist/fonts",
          outputPath: "/fonts",
        },
      },
    ],
  },
  // devServer: {
  //   contentBase: './dist'
  // },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
    }),
    new MiniCssExtractPlugin({
      filename: "[name].bundle.css",
      path: path.resolve(__dirname, "dist"),
    }),
  ],
  resolve: {
    extensions: [".js"],
  },
};
