# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0-rc.2] - 2020-07-08
### Changed
- /support command update
- fix bug in binary_search

## [0.2.0-rc.1] - 2020-07-07
### Added
- Stickers support
- /clean_errors command in DEBUG mode
- /chat_id command for getting chat if in DEBUG mode
- Timeouts in /level command
- Cases in russian translation
- Donations
- /license command with license and copyright info
### Changed
- Bug fixies
- Made some optimizations: some configs are now loading once, using binary search on karma levels, statick karma levels check on start
- Now different login and 'from email' can be used
- Build is now short hash of last commit
- Now you can't decrease karma of user, who have just decreased your karma
- Remove mentions from /top and /antitop commands
- Move administrators and karma change phrases lists to configs

## [0.1.1] - 2020-07-06
### Changed
- Fix karma range config

## [0.1.0] - 2020-07-06
### Changed
- Bug fixes

## [0.1.0-rc.1] - 2020-06-18
### Added
- New messages that change karma
- New /help command
- Add welcome messages
### Changed
- Bug fixes: all data is automaticly migrated after group migration to supergroup
- Typo fixes
- Now you can't use some bot commands in private messages

## [0.1.0-beta.3] - 2020-06-16
### Changed
- Typo fixed

## [0.1.0-beta.2] - 2020-06-16
### Added
- Announcements: send custom messages to all chats
- Karma levels: each level has its own rights!
- You can now create sample error in debug mode
- Get top and antitop of users in group
### Changed
- Bug fixes
- Made some optimizations: now config parsers are singletons
- Improved error managing system: now errors from handlers are reported too
- Now you can't change user's karma for same message twice
## [0.1.0-beta.1] - 2020-06-15
### Added
- Error managing system
- Logging
- Increase and decrease karma
- Russian language

[0.1.0-beta.2]: https://github.com/sandsbit/skarmabot/compare/v0.1.0-beta.1...v0.1.0-beta.2
[0.1.0-beta.3]: https://github.com/sandsbit/skarmabot/compare/v0.1.0-beta.2...v0.1.0-beta.3
[0.1.0-rc.1]: https://github.com/sandsbit/skarmabot/compare/v0.1.0-beta.3...v0.1.0-rc.1
[0.1.0]: https://github.com/sandsbit/skarmabot/compare/v0.1.0-rc.1...v0.1.0
[0.1.1]: https://github.com/sandsbit/skarmabot/compare/v0.1.0...v0.1.1
[0.2.0-rc.1]: https://github.com/sandsbit/skarmabot/compare/v0.1.1...v0.2.0-rc.1
[0.2.0-rc.2]: https://github.com/sandsbit/skarmabot/compare/v0.2.0-rc.1...v0.2.0-rc.2
