const mongoose = require('mongoose');

const RepoSchema = new mongoose.Schema({
  name: {
    type: String,
    require: true
  },
  stargazers_count: {
    type: Number,
    default:0
  },
  forks_count:{
    type: Number,
    default:0
  },
  open_issues_count: {
    type: Number,
    default: 0
  },
  closed_issues_count: {
    type: Number,
    default: 0
  },
  score: {
    type: Number,
    default:0
  },
  languages: {
    type: [String],
    default: []
  },
  about: {
    type: String,
    default: ""
  },
  tags: {
    type: [String],
    default: []
  }
});

mongoose.model("Repo", RepoSchema);